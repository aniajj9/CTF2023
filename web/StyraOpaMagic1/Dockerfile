FROM golang AS builder

WORKDIR /app
ENV CGO_ENABLED=0

COPY go.mod go.sum ./
RUN go mod download && go mod verify

COPY main.go /app/main.go
RUN go build -o /app/ctf /app

FROM alpine

COPY --from=builder /app/ctf /ctf
COPY assets /assets

CMD ["/ctf", "-assets=/assets"]
