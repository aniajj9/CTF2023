const calculate = async (data) => {
    const result = await fetch("/calculate", {
        method: "POST",
        body: new URLSearchParams(data)
    })

    return await result.text()
}

const onSubmit = async (event) => {
    event.preventDefault()
    const resultContainer = document.getElementById("result")
    resultContainer.innerText = "Calculating..."

    const data = new FormData(event.target)
    const result = await calculate(data)
    
    resultContainer.innerText = result
}

const main = () => {
    const form = document.getElementById("calculator");
    form.addEventListener("submit", onSubmit);
}

main()