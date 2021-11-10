import React from 'react';
import './scoped.css';
import VoicEmail from '../../img/VoicEmail.png';
import FootImg from '../../img/foot.png';
import ChatBox from '../ChatBox/index';

const App = () => {
  return (
    < div className="App" >
      < div className="container" >
        <div className="nav-bar">
          <img style={{height:50,paddingRight:15}} src={VoicEmail} alt="voicemail"></img>
          LinguAI - VoicEmail Assistant
          <div className="nav-text"></div>
        </div>
        <div className="chat-box-container">
          <ChatBox></ChatBox>
        </div>
        {/* <div className="foot">
          <img style={{ height: 50 }} src={FootImg}></img>
        </div> */}
      </div >
    </div >
  );
}

export default App;
