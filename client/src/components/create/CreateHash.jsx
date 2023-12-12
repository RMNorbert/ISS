import { useState } from "react";
import "./Card.css"

function CreateHash () {
    const [isHidden, setIsHidden] = useState (true);
    const [hash, setHash] = useState('');
    const [acceptType, setAcceptType] = useState('application/json');
    const [formData, setFormData] = useState({
        secret: '',
        expire_after_views: 0,
        expire_after: 0,
    });
    
    const  HandleSubmit = async (e) => {
        e.preventDefault();
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
                                onChange={handleChange}
                            />
                        </div>
                        <div className="inputBox">
                            <label htmlFor="expire_after">Secret expire after minutes:</label>
                            <input type="number" id="expire_after"
                             placeholder="if it is set to 0 then the secret wont expire by time"
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
                </div>
                <div className="hash" style={{ display: isHidden ? "none" : "block"}}>
                    <h3>The hash you can share your secret with :</h3>
                    {hash && hash}
                </div>
        </div>
    )
}

export default CreateHash;