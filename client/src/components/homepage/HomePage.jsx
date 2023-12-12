import CreateLink from "../create/CreateLink";
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
            <CreateLink />
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