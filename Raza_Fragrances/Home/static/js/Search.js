
const url = window.location.href
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')
const resultBox = document.getElementById('result-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value


const sendSearchData = (Fragrance) => {
    $.ajax({
        type: 'POST',
        url: 'Search-results/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'Fragrance': Fragrance,
        },
        success: (res) => {
            const data = res.data
            if (Array.isArray(data)){
                resultBox.innerHTML =""
                data.forEach(Fragrance => {
                    resultBox.innerHTML+= `
                        <a href="/Product-details/${Fragrance.pk}" class="text-dark text-decoration-none item">
                            <div class="row p-2">
                                <div class="col-md-1 col-3">
                                    <img class="img-fluid" src="${Fragrance.image}">
                                </div>
                                <div class="col-md-10 col-9 d-flex align-items-center">
                                    <p class="float-start Ec-Searched-Product-Title">${Fragrance.Title}</p>
                                </div>
                            </div>
                        </a>
                    `
                })
            }
            else{
                if (searchInput.value.length > 0){
                    resultBox.innerHTML =  `<b>${data}</b>`
                }
                else{
                    resultBox.classList.add('Ec-not-visible')
                }
            }
        },
        error: (error) => {
            console.log(error)
        },
    })
}



searchInput.addEventListener('keyup', e=>{
    console.log(e.target.value)
    if (resultBox.classList.contains('Ec-not-visible')){
        resultBox.classList.remove('Ec-not-visible')
    }

    sendSearchData(e.target.value)
})