const object1 = document.getElementById("s1")
const liste1 = document.getElementsByClassName("s1")
const object1_1 = document.getElementById("s1_1")
const liste1_1 = document.getElementsByClassName("s1_1")
const object1_1_1 = document.getElementById("s1_1_1")
const liste1_1_1 = document.getElementsByClassName("s1_1_1")
const object1_1_2 = document.getElementById("s1_1_2")
const liste1_1_2 = document.getElementsByClassName("s1_1_2")
const object2 = document.getElementById("s2")
const liste2 = document.getElementsByClassName("s2")
function sous_classe(obj, liste) {
    if (liste[0].style.display == "none") {
        for (let i = 0; i < liste.length; i++) {
            liste[i].style.display = "block";
            obj.style.transform = "rotate(180deg)";
            console.log("lalaa")
            // ouvert1 = 0
        }
    } else {
        for (let i = 0; i < liste.length; i++) {
            liste[i].style.display = "none";
            obj.style.transform = "rotate(0deg)";
            // ouvert1 = 1
        }
    }
}

object1.onclick = function() {
    sous_classe(object1, liste1)
};
       
object1_1.onclick = function() {
    sous_classe(object1_1, liste1_1)
};          
object1_1_1.onclick = function() {
    sous_classe(object1_1_1, liste1_1_1)
};          
object1_1_2.onclick = function() {
    sous_classe(object1_1_2, liste1_1_2)
};          
object2.onclick = function() {
    sous_classe(object2, liste2)
};          
