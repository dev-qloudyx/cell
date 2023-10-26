const disable_option = (id_select, num_option) =>{
    document.querySelector(`${id_select} option:nth-child(${num_option})`).disabled = true;
}

disable_option("#id_freezer", "3");
disable_option("#id_freezer", "4");
disable_option("#id_freezer", "6");

disable_option("#id_container", "2");

disable_option("#id_subcontainer", "2");
disable_option("#id_subcontainer", "4");

disable_option("#id_fill", "3");
disable_option("#id_fill", "4");
disable_option("#id_fill", "5");

disable_option("#id_biomixture", "2");
disable_option("#id_biomixture", "4");

disable_option("#id_solutefraction", "5");

disable_option("#id_cooling", "2");
disable_option("#id_cooling", "4");

function addClass(divname) {
    var element = document.getElementById(divname);
    element.classList.add("form-select");
 }

addClass("id_freezer");
addClass("id_container");
addClass("id_subcontainer");
addClass("id_fill");
addClass("id_biomixture");
addClass("id_solutefraction");
addClass("id_transitiontemp");
document.getElementById("id_transitiontemp").style.background = '#ced5dd82';
document.getElementById("id_transitiontemp").style.color = 'rgb(136, 136, 136)';
addClass("id_cooling");
addClass("id_finaltemp");
document.getElementById("id_finaltemp").style.background = '#ced5dd82';
document.getElementById("id_finaltemp").style.color = 'rgb(136, 136, 136)';


const elements = document.querySelectorAll("select");
document.querySelector(`.btn`).disabled = true;

for (let i = 1; i < elements.length; i++) {
    elements[i].disabled = true;
  }
let count2 = 0;
const show2 = () => {
    const currentSelect = elements[count2];
    const nextSelect = elements[count2 + 1];
    
    if (currentSelect && nextSelect && count2 < 7) {
        nextSelect.disabled = false;
        currentSelect.removeEventListener("change", show2);
        nextSelect.addEventListener("change", show2);
        count2++;

        
    }
    if(currentSelect == elements[6]){
        document.querySelector(`.btn`).disabled = false;
        currentSelect.removeEventListener("change", show2);
    }
}

elements[0].addEventListener("change", show2);