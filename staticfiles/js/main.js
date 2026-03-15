document.addEventListener("DOMContentLoaded", () => {
  // Переключение вкладок профиля
  const tabButtons = document.querySelectorAll(".tab-btn")
  tabButtons.forEach((btn) => {
    btn.addEventListener("click", function () {
      tabButtons.forEach((b) => b.classList.remove("active"))
      this.classList.add("active")
    })
  })

  // Лайки
  const likeBtns = document.querySelectorAll(".like-btn")
  likeBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const heart = this.querySelector(".heart")
      if (heart) {
        if (heart.textContent === "♡") {
          heart.textContent = "♥"
        } else {
          heart.textContent = "♡"
        }
      }
    })
  })

  // CSRF токен для Django
  function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";")
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }

  const csrftoken = getCookie("csrftoken")
  console.log("CSRF Token:", csrftoken)
})
