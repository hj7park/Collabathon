function overlay() {
	el = document.getElementById("overlay");
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}

function overlay2() {
	el = document.getElementById("overlay2");
	console.log(el)
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}