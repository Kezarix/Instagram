// File handling
const uploadArea = document.getElementById("uploadArea")
const fileInput = document.getElementById("fileInput")
const previewSection = document.getElementById("previewSection")
const previewImage = document.getElementById("previewImage")
const previewVideo = document.getElementById("previewVideo")

// Drag and drop
uploadArea.addEventListener("click", () => fileInput.click())

uploadArea.addEventListener("dragover", (e) => {
  e.preventDefault()
  uploadArea.classList.add("dragover")
})

uploadArea.addEventListener("dragleave", () => {
  uploadArea.classList.remove("dragover")
})

uploadArea.addEventListener("drop", (e) => {
  e.preventDefault()
  uploadArea.classList.remove("dragover")
  const files = e.dataTransfer.files
  handleFiles(files)
})

fileInput.addEventListener("change", (e) => {
  handleFiles(e.target.files)
})

function handleFiles(files) {
  if (files.length === 0) return

  const file = files[0]
  const reader = new FileReader()

  reader.onload = (e) => {
    if (file.type.startsWith("image/")) {
      previewImage.src = e.target.result
      previewImage.style.display = "block"
      previewVideo.style.display = "none"
    } else if (file.type.startsWith("video/")) {
      previewVideo.src = e.target.result
      previewVideo.style.display = "block"
      previewImage.style.display = "none"
    }

    uploadArea.style.display = "none"
    previewSection.style.display = "block"
  }

  reader.readAsDataURL(file)
}

// Caption counter
const captionInput = document.getElementById("caption")
const charCount = document.getElementById("charCount")

captionInput.addEventListener("input", () => {
  charCount.textContent = captionInput.value.length
})

// Content type switching
function switchContentType(type) {
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.classList.remove("active")
  })
  event.target.classList.add("active")
  console.log("Content type switched to:", type)
}

// Filter selection
document.querySelectorAll(".filter-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".filter-btn").forEach((b) => b.classList.remove("active"))
    btn.classList.add("active")
  })
})

// Publish and save functions
function publishPost() {
  const caption = captionInput.value
  const allowComments = !document.getElementById("allowComments").checked
  const hideLikes = document.getElementById("hideLikes").checked

  if (!fileInput.files[0]) {
    alert("Please select an image or video")
    return
  }

  console.log("Publishing post:", { caption, allowComments, hideLikes })
  alert("Post published successfully!")
}

