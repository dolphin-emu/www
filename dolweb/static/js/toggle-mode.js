// Mode toggling built with help from https://css-tricks.com/author/mohamedadhuham/ 
// on https://css-tricks.com/a-complete-guide-to-dark-mode-on-the-web/



//////////// Var Initialization //////////////

// Select the icon
const sunMoon = document.querySelector("#sunMoon")

// set alternative icon styles
const sun = ' <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sun"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>'
const moon =' <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="feather feather-moon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>'

// select the current css theme
const cssSheet = document.querySelector("#theme-link")

// Check for dark mode preference on the browser/os preference
// returns boolean in ".matches" attribute
const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)")

// Get the user's theme preference from local storage, if there
const currentTheme = localStorage.getItem("theme")


/////// Check for theme on intial page load (local storage or os/browser preference) /////////

// run on page load
$(document).ready(function(){
  // 1. if the user has a set mode in their local storage use it
  if (currentTheme == "dark") {
    sunMoon.innerHTML = sun
    cssSheet.href = "../m/static/css/dolphin-dark.css"

  // 2. Otherwise check if light mode is set in localstorage
  } else if (currentTheme=="light"){
    sunMoon.innerHTML = moon
    cssSheet.href = "../m/static/css/dolphin-light.css"
  }

  // 3. Otherwise check if the user has a default OS/Browser mode preference
  // could remove os/browser checks as desired and just default to light in above step 2
  else if (prefersDarkScheme.matches==true){
    sunMoon.innerHTML = sun
    cssSheet.href = "../m/static/css/dolphin-dark.css"
  }
  // 4. default to light mode
  else {
    sunMoon.innerHTML = moon
    cssSheet.href = "../m/static/css/dolphin-light.css"
  }
});


///////// Handle icon click events/requests to change the mode to light or dark //////////

// Event that activates when sun or moon is clicked. 
// Minor optimization of # of resize calls can be done with throttle wrapper around 
// After testing, didn't seem worth it
sunMoon.addEventListener("click", function() {
  // If light mode is already set as the href, then change it to dark mode
  if (!cssSheet.href.includes("dolphin-light.css")) {
    sunMoon.innerHTML = moon
    cssSheet.href = "../m/static/css/dolphin-light.css"
    var theme = 'light'
    
  // otherwise the theme is currently dark and needs to change it to light mode
  } else {
    sunMoon.innerHTML = sun
    cssSheet.href = "../m/static/css/dolphin-dark.css"
    var theme = 'dark'
  }
  // Lastly, save the  current preference to localStorage to keep using it on new page requests/other pages
  localStorage.setItem("theme", theme)
  
})



////// Move light/dark icons between mobile and desktop view ///////

// toggle where the dark/light mode icon appears
const lastNavbarLi = document.querySelector("#lastNavbarLi")
const hamburger = document.querySelector("#hamburger")

function moveSunMoon(){
  // if window width indicates mobile view
  if  (window.innerWidth < 768) {
    sunMoon.remove()
    hamburger.after(sunMoon)
 }
 // else in desktop view
  else {
    sunMoon.remove()
    lastNavbarLi.after(sunMoon)
  }
}

// bootstrap switches between mobile and desktop at 768 px by default
// call moveSunMoon function when first loading the page and when the page is resized

// if window resize call 
$(window).resize(function() {
  moveSunMoon()
});

// run when document loads
$(document).ready(function() {
  moveSunMoon()
});