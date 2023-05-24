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

const sous_classe = (obj, liste) => {
    if (Array("", "none").includes(liste[0].style.display)) {
        for (let i = 0; i < liste.length; i++) {
            liste[i].style.display = "block";
            obj.style.transform = "rotate(180deg)";
        }
    } else {
        for (let i = 0; i < liste.length; i++) {
            liste[i].style.display = "none";
            obj.style.transform = "rotate(0deg)";
        }
    }
}

object1.onclick = () => {
    sous_classe(object1, liste1)
};

object1_1.onclick = () => {
    sous_classe(object1_1, liste1_1)
};
object1_1_1.onclick = () => {
    sous_classe(object1_1_1, liste1_1_1)
};
object1_1_2.onclick = () => {
    sous_classe(object1_1_2, liste1_1_2)
};
object2.onclick = () => {
    sous_classe(object2, liste2)
};

