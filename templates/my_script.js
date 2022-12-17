function testDisable() {
    const etat = document.getElementById("etat");
    const dateElt = document.getElementById("date_fin");
    const date = new Date();
    const current_date = date.getFullYear()+"-"+(date.getMonth()+1)+"-"+ date.getDate();
    if (etat.value !== "1" && dateElt.value === ""){
        dateElt.value = current_date
    }
}
function testColor(id){
    if (id === "1"){
        return "priorite1"
    } else if (id === "2"){
        return "priorite2"
    } else {
        return "priorite3"
    }
}
let selection = document.getElementById("selection_categorie");
if ("{{ tache[1] }}" === "Travail"){
    selection.value = "1";
} else{
    selection.value = "2";
}
selection = document.getElementById("priorite");
if ("{{ tache[3] }}" === "Basse"){
    selection.selectedIndex = 0;
} else if ("{{ tache[3] }}" === "Moyenne"){
    selection.selectedIndex = 1;
} else{
    selection.selectedIndex = 2;
}
selection = document.getElementById("etat");
if ("{{ tache[2] }}" === "En cours"){
    selection.selectedIndex = 0;
} else if ("{{ tache[2] }}" === "Terminée"){
    selection.selectedIndex = 1;
} else {
    selection.selectedIndex = 2;
}
testDisable()