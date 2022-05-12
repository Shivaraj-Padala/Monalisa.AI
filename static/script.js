let speakBtn = document.getElementById('speakMsgBtn');
let sendMsgBtnEl = document.getElementById('sendMsgBtn');
let chatContainerEl = document.getElementById('chatContainer');
let userInputEl = document.getElementById('userInput');

var msg = window.speechSynthesis;

window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition || window.oSpeechRecognition;
const recognition = new window.SpeechRecognition();

let enterButton = document.addEventListener('keydown', function(e) {
    if(e.key === 'Enter'){
        getChat();
    }
});

function browserSpeak(speechText){
    msg.speak(new SpeechSynthesisUtterance(speechText));
}

function getChat() {
    val = userInputEl.value;
    userInputEl.value = "";
    if (val){
        createchat(val); 
    } else {
        browserSpeak("can't send empty messages");
    }
}

sendMsgBtnEl.addEventListener("click", getChat);
speakBtn.addEventListener("click", function(){
    if ('SpeechRecognition' in window) {
        console.log('supported speech')
    } else {
        browserSpeak('Speech recognition is not supported by the browser');
    }

    recognition.continuous = false;

    recognition.onresult = (event) => {
      var data = event.results[event.results.length -1][0].transcript
      userInputEl.value = data;
      setTimeout(() => { getChat(); }, 500);
    }

    recognition.onspeechend = function() {
        console.log("speech ended")
    }
    recognition.start();
});

function appendReply(rep){
    let chatmsg = rep;
    let outer_div = document.createElement('div')
    outer_div.classList.add("d-flex", "flex-row");
    let profile_div = document.createElement('div')
    profile_div.classList.add("chat-dp", "mt-2", "mr-2")
    let span = document.createElement('span');
    span.classList.add('msg-from-chatbot');
    span.textContent = chatmsg;
    outer_div.appendChild(profile_div);
    outer_div.appendChild(span);
    chatContainerEl.appendChild(outer_div);
    window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);

}

function getReply(rep) {

    if(rep.includes('translatedText')){
        browserSpeak('Here is your translation');
        botMsg = rep.replace('translatedText','');
        appendReply(botMsg);
    } else if(rep.includes('news-Data')){
        browserSpeak('here are the top news headlines');
        newsArray = rep.split('\n\n')
        for(newsData = 0; newsData < newsArray.length-1; newsData++ ){
            appendReply(newsArray[newsData].replace('news-Data',''));
        }
    }else{
        browserSpeak(rep);
        appendReply(rep);
    }
    
}

getReply('Monalisa is ready to roll !');
getReply('how can i help you ?');

function createchat(txt) {
    let outer_div = document.createElement('div');
    let span = document.createElement('span');
    let profile_div = document.createElement('div');

    outer_div.classList.add("d-flex", "flex-row", "justify-content-end");
    profile_div.classList.add("chat-dp-user", "mt-2", "ml-2")
    span.classList.add('msg-to-chatbot');
    span.textContent = txt;
    outer_div.appendChild(span);
    outer_div.appendChild(profile_div);
    chatContainer.appendChild(outer_div);

    window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);

    if(txt.includes('+')){
        finalTxt ='';
        for(i=0; i<=txt.length-1; i++){
            finalTxt += txt[i].replace('+','addopcode');
        }
    }else{
        finalTxt = txt;
    }

    let userReq = fetch(`http://127.0.0.1:5000/api?query=${finalTxt}`)

    userReq.then(resp=>{
        return resp.text()
    }).then(bResponse =>{
        getReply(bResponse)
    })
}