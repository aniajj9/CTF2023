package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"html/template"
	"io"
	"log"
	"net/http"
	"os"
	"path"
	"strconv"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

type errResponse struct {
	Error string `json:"error"`
}

type taskData struct {
	Rego       string
	Endpoint   string
	TaskNumber int
	JSONData   string
}

func main() {
	var assetsPath string
	flag.StringVar(&assetsPath, "assets", "./assets", "path to folder containing assets")
	flag.Parse()

	t, err := template.ParseGlob(path.Join(assetsPath, "*.html"))
	if err != nil {
		log.Fatal(err)
	}
	for _, tmpl := range t.Templates() {
		log.Println(tmpl.Name())
	}

	regos := make([]string, 5)
	for i := range regos {
		bs, err := os.ReadFile(path.Join(assetsPath, fmt.Sprintf("task%d.rego", i)))
		if err != nil {
			log.Fatal(err)
		}
		regos[i] = string(bs)
	}

	datas := make([]string, len(regos))
	for i := range datas {
		bs, err := os.ReadFile(path.Join(assetsPath, fmt.Sprintf("data%d.json", i)))
		if err != nil {
			log.Fatal(err)
		}
		datas[i] = string(bs)
	}

	r := chi.NewRouter()
	hc := http.Client{}
	r.Use(middleware.Logger)
	r.Get("/task/{taskNumber}", func(w http.ResponseWriter, r *http.Request) {
		taskStr := chi.URLParam(r, "taskNumber")
		task, err := strconv.Atoi(taskStr)
		if err != nil {
			json.NewEncoder(w).Encode(errResponse{Error: err.Error()})
			w.WriteHeader(http.StatusBadRequest)
			return
		}
		if task < 0 || task > 4 {
			json.NewEncoder(w).Encode(errResponse{Error: "task should be between 0-4"})
			w.WriteHeader(http.StatusBadRequest)
			return
		}

		data := taskData{
			Rego:       regos[task],
			JSONData:   datas[task],
			Endpoint:   path.Join("/task", taskStr),
			TaskNumber: task,
		}

		if err := t.ExecuteTemplate(w, "task.html", data); err != nil {
			log.Println(err)
			w.WriteHeader(http.StatusInternalServerError)
		}
	})

	r.Post("/task/{taskNumber}", func(w http.ResponseWriter, r *http.Request) {
		taskStr := chi.URLParam(r, "taskNumber")
		task, err := strconv.Atoi(taskStr)
		if err != nil {
			json.NewEncoder(w).Encode(errResponse{Error: err.Error()})
			w.WriteHeader(http.StatusBadRequest)
			return
		}
		if task < 0 || task > 4 {
			json.NewEncoder(w).Encode(errResponse{Error: "task should be between 0-4"})
			w.WriteHeader(http.StatusBadRequest)
			return
		}

		req, err := http.NewRequest("POST", fmt.Sprintf("http://20.123.50.13:8181/v1/data/ctf/task%d/decision", task), r.Body)
		defer r.Body.Close()
		if err != nil {
			log.Println(err)
			w.WriteHeader(http.StatusInternalServerError)
			return
		}

		res, err := hc.Do(req)
		if err != nil {
			json.NewEncoder(w).Encode(errResponse{
				Error: err.Error(),
			})
			w.WriteHeader(http.StatusInternalServerError)
			return
		}

		log.Println(res.StatusCode)

		jsonBs, err := io.ReadAll(res.Body)
		if err != nil {
			log.Println(err)
			w.WriteHeader(http.StatusInternalServerError)
			return
		}

		var buf bytes.Buffer
		if err := json.Indent(&buf, jsonBs, "", "  "); err != nil {
			log.Println(err)
			w.WriteHeader(http.StatusInternalServerError)
			return
		}

		_, err = io.Copy(w, &buf)
		defer res.Body.Close()
		if err != nil {
			log.Println(err)
			w.WriteHeader(http.StatusInternalServerError)
		}
		w.WriteHeader(res.StatusCode)
	})

	http.ListenAndServe(":3000", r)
}
