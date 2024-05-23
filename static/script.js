function toggleDescription(index) {
    var dots = document.getElementById("dots-" + index);
    var moreText = document.getElementById("more-" + index);
    var btnText = document.getElementById("myBtn-" + index);

    if (dots.style.display === "none") {
        dots.style.display = "inline";
        btnText.innerHTML = "Read more";
        moreText.style.display = "none";
    } else {
        dots.style.display = "none";
        btnText.innerHTML = "Read less";
        moreText.style.display = "inline";
    }
}

var sidenav = document.getElementById("mySidenav");
var openBtn = document.getElementById("openBtn");
var closeBtn = document.getElementById("closeBtn");

openBtn.onclick = openNav;
closeBtn.onclick = closeNav;

function openNav() {
    sidenav.classList.add("active");
}

function closeNav() {
    sidenav.classList.remove("active");
}

document.addEventListener('DOMContentLoaded', () => {
    const starsOuter = document.querySelectorAll('.stars-outer');
    starsOuter.forEach(starOuter => {
      const score = parseFloat(starOuter.nextSibling.textContent.trim().match(/\((\d+(\.\d+)?)\)/)[1]);
      const starInner = starOuter.querySelector('.stars-inner');
      const starPercentage = (score / 5) * 100;
      starInner.style.width = `${starPercentage}%`;
    });
  });
  