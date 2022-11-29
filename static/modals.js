var modal = document.getElementById('simpleModal');

//var modalBtn = document.getElementById('modalBtn');

var modalCloseBtn = document.getElementsByClassName('modalCloseBtn')[0];

//modalBtn.addEventListener('click', openModal);
modalCloseBtn.addEventListener('click', closeModal);
window.addEventListener('click', clickOutside);

/*
function openModal(){
    modal.style.display = 'block';
}
*/

function closeModal() {
    modal.style.display = 'none';   
}

function clickOutside(e) {
    if(e.target == modal) {
        modal.style.display = 'none';
    }
}