import CreateHash from "../create/CreateHash";
import "./HomePage.css";
import background from "../../assets/background.mp4"
import { useNavigate } from "react-router-dom";
function HomePage() {
    const navigate = useNavigate();

    return (
        <div className="page">
        <div className="home">
        <video src={background} autoPlay muted loop id="myVideo"/>
            <div className="homeContent">
            <CreateHash />
            <button
                onClick={() => navigate("/retrieve")}
            >
                Retrieve page
            </button>
            </div>
        </div>
        </div>
    )
}

export default HomePage;