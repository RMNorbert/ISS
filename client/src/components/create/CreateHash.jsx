import { useState } from "react";
import "./Card.css"

function CreateHash () {
    const [isHidden, setIsHidden] = useState (true);
    const [messageHidden, setMessageHidden] = useState (true);
    const [message, setMessage] = useState ('');
    const [hash, setHash] = useState('');
    const [acceptType, setAcceptType] = useState('application/json');
    const [formData, setFormData] = useState({
        secret: '',
        expire_after_views: 1,
        expire_after: 0,
    });
    
    function dataIsInvalid() {
        let isInValid = true;
        if(formData.secret.length < 1 ){
            setMessage("Secret cannot be empty")
            return isInValid;
        }

        if(formData.expire_after_views < 1 ) {
            setMessage("Secret cannot be shared with less than 1 views")
            return isInValid;
        }
         
        if(formData.expire_after < 0) {
            setMessage("Secret cannot be shared with less 1 minute to live")
            return isInValid;
        }
        return false;
    }

    const  HandleSubmit = async (e) => {
        e.preventDefault();
        if(dataIsInvalid()){
            setMessageHidden(false)
            return;
        }
        const url = '/v1/secret';
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': acceptType
            },
            body: new URLSearchParams(formData).toString(),
        };        
        try {
            const response = await fetch(url, requestOptions);
            if(response.status === 200){
                if (acceptType === "application/json") {
                    const data = await response.json();
                    setHash(data);
                } else if (acceptType === "application/xml") {
                    const data = await response.text();
                    const parser = new DOMParser();
                    const xmlDoc = parser.parseFromString(data, "application/xml");
                    const secretElement = xmlDoc.querySelector("response").textContent;
                    setHash(secretElement);
                  }
                setIsHidden(false);
            }
        } catch (error) {
            setIsHidden(true);
            console.error('Error:', error);
        }
    }

    const handleChange = (event) => {
        const { id, value } = event.target;
        setFormData((prevFormData) => ({
            ...prevFormData,
            [id]: value,
        }));
    };

    return(
        <div className="box">
            <div style={{ display: isHidden ? "block" : "none" }}>
            <h1>Register a secret</h1>
                <div className="elements">
                    <form onSubmit={HandleSubmit}>
                        <div className="inputBox">
                            <label htmlFor="secret">Secret:</label>
                            <input type="text" id="secret"
                                value={formData.secret}
                                onChange={handleChange}
                            />
                        </div>
                        <div className="inputBox">
                            <label htmlFor="expire_after_views">Secret expire after number of views:</label>
                            <input type="number"id="expire_after_views"
                                value={formData.expire_after_views}
                                min={1}
                                onChange={handleChange}
                            />
                        </div>
                        <div className="inputBox">
                            <label htmlFor="expire_after">Secret expire after minutes:</label>
                            <input type="number" id="expire_after"
                                min={0}
                                //placeholder="if it is set to 0 then the secret wont expire by time"
                                value={formData.expire_after}
                                onChange={handleChange}
                             />
                        </div>
                        <div className="inputBox">
                            <label htmlFor="expire_after">Select response type:</label>
                            <select
                                value={acceptType}
                                onChange={(event) => {setAcceptType(event.target.value)}}
                            >
                                <option>application/json</option>
                                <option>application/xml</option>
                            </select>
                        </div>
                        <button className="inputBox" type="submit">
                            Register
                        </button>
                    </form>
                </div>
                    <h3 className="message"
                        style={{ display: messageHidden ? "none" : "block" }}
                    >{message}
                    </h3>
                </div>
                <div className="hash" style={{ display: isHidden ? "none" : "block"}}>
                    <h3>The hash you can share your secret with :</h3>
                    <h4>{hash && hash}</h4>
                    <button
                    onClick={() => {navigator.clipboard.writeText(hash)}}
                    >
                        Copy
                    </button>
                    
                    <button onClick={() => setIsHidden(true)}>Return</button>
                </div>
        </div>
    )
}

export default CreateHash;