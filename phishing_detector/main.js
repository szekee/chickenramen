import './style.css'

const video = document.querySelector('#video')
const btn = document.querySelector('#btn')
const canvas =  document.querySelector('#canvas')

if(navigator.mediaDevices.getUserMedia){
    navigator.mediaDevices.getUserMedia({video: true })

    .then(stream => {
        video.srcObject = stream
    })
    .catch(error => {
        console.log('An error occured while accessing webcam.')
    })
}

btn.addEventListener('click', () => {
    // get intrinsic width and height of the video element
    const width = video.videoWidth, height = video.videoHeight

    const context = canvas.getContext('2d')

    canvas.width = width
    canvas.height = height

    context.drawImage(video, 0, 0, width, height)

    const imgURL = canvas.toDataURL('image/png')

    console.log(imgURL)
    const image_url = js_to_image(imgURL)

    document.getElementById("url").value = image_url

})

function js_to_image(imgURL) {
    fetch("http://localhost:5000/tourl/", {
        method: 'POST',
        body: JSON.stringify({
            data: imgURL
        })
    })
    .then(function(response) {
        console.log(response.json())
        return response.json();
    })
    .catch(function(err) {
        console.log(err)
    });
}



const submitBtn = document.getElementById('submit')
submitBtn.addEventListener('click', () => {
    const url = document.getElementById('url');

    fetch("http://localhost:5000/checkurl/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "url": url
        })
    })
    .then(function(response) {
        console.log(response.json())
        return response.json();
    })
    .catch(function(err) {
        console.log(err)
    });
})