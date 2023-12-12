import { useEffect, useState } from "react";

function RetrievePage() {
    const [hash, setHash] = useState("");
    const [secret, setSecret] = useState("");
    const [fetched, setFetched] = useState(false);
    const [type, setType] = useState("application/json");
    const [isHidden, setIsHidden] = useState(true);


    async function getSecret() {
        const url = `/v1/secret/${hash}`;
        try {
            const response = await fetch(url, {
                headers: {
                    Accept: type,
                },
            });
            if (response.ok) {
                if (type === "application/json") {
                    const data = await response.json();
                    setSecret(data);
                    setFetched(true);
                }
                if (type === "application/xml") {
                    const data = await response.text();
                    const parser = new DOMParser();
                    const xmlDoc = parser.parseFromString(
                        data,
                        "application/xml"
                    );
                    const secretValue =
                        xmlDoc.querySelector("response").textContent;

                    setSecret(secretValue);
                    setFetched(true);
                }
            } else {
                console.error("Error fetching secret:", response);
                setIsHidden(false)
            }
        } catch (error) {
            console.error("Error:", error);
        }

    }
    useEffect(() => {
        
    }, []);

    
        return (
        <div className="home">
            <div className="homeContent">
            <div className="inputBox">
                <label>Select response type:</label>
                <select
                    value={type}
                    onChange={(event) => {
                        setType(event.target.value);
                    }}
                >
                    <option>application/json</option>
                    <option>application/xml</option>
                </select>
                <div className="inputBox">
                            <label htmlFor="hash">Hash:</label>
                            <input type="text"
                                onChange={(event) => {
                                    setHash(event.target.value);
                                }}
                            />
                </div>
                <button
                    onClick={() => getSecret()}
                >
                    Retrieve secret
                </button>   
            </div>
            {fetched && 
            <div className="retrieved">
                    <h1>Here is the retrieved secret:</h1>
                    <h1 className="card">{secret}</h1>
                    <button
                    onClick={() => {navigator.clipboard.writeText(secret)}}
                    >
                        Copy
                    </button>
            </div>}
            <h3 
                style={{ display: isHidden ? "none" : "block" }}>
                Hash cannot be retrieved
            </h3>
            </div>
        </div>
        );
    }

export default RetrievePage;
