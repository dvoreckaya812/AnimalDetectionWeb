var show = false;
var low_op = 0.8;
var high_op = 1.0;

$('#side-button').click(function () {
    _showSidePanel();
});

$('#side-content').hover(function (){
    if (show === true){
        $('#side-content').animate({
            opacity: high_op,
        }, 300)
    }
}, function (){
    if (show === true){
        $('#side-content').animate({
            opacity: low_op,
        }, 300)
    }
});

function showSidePanel(){
    show = false;
    _showSidePanel();
}

function _showSidePanel(){
    $('#side-content').animate({
        width: (show === false) ? "35vw" : "0vw",
    }, 300, function (){
        if (show === true) {
            show = false;
            $('#side-button').html('<');
        }
        else{
            show = true;
            $('#side-button').html('>');
        }
    });
}

function showFile(input) {
  let file = input.files[0];
  let img_result = document.getElementById("image_result");
  let video_result = document.getElementById("video_result")
  let title = document.getElementById("title")
  let filename = document.getElementById("filename")
  filename.innerText = file.name;
  if (file.type.startsWith("video")){
      video_result.classList.remove('hidden')
      video_result.classList.add('visible')
      img_result.classList.add('hidden')
      video_result.src = URL.createObjectURL(file)
      img_result.src = undefined

  }
  if (file.type.startsWith("image")){
      img_result.classList.remove('hidden')
      img_result.classList.add('visible')
      video_result.classList.add('hidden')
      img_result.src = URL.createObjectURL(file);
      video_result.src = undefined
  }
  title.innerText = "Готово к обработке";
  title.classList.remove("loading");
  title.classList.remove("borders-wait")
  title.classList.add("borders-ready");
  $('#upload').closest('.input-file').find('.input-file-text').html(file.name);
  let button = document.getElementsByClassName('button')[0];
  button.classList.add('clickplz');
  button.removeAttribute('disabled')
}

function removeClasses(){
    setTimeout(function () {
        $("#main-menu").children().removeClass(function (index, className) {
            return (className.match(/(^|\s)revealator-\S+/g) || []).join(' ')
        })
    }, 2500)

}

window.onload = removeClasses


    //$("#main-menu").children('li').removeClass(function (index, className) {
    //    return (className.match(/(^|\s)revealator-\S+/g) || []).join(' ')
    //})
