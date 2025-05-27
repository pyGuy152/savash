

import { useEffect, useRef } from "react";
import { apiUrl, getToken, LOGOUT } from "../types";
import "./HomeNav.css";

import { Link, useNavigate } from "react-router-dom";




function TeacherNav() {
  const navigate = useNavigate();
  const inboxIcon = useRef(null);

  function handleLogout(){
    LOGOUT();
    navigate("/");
  }

  function newMessage(){
      fetch(apiUrl + "/users/", {
          method: "GET",
          headers: {
            Authorization: "bearer " + getToken(document.cookie),
          },
        })
        .then((res) => res.json())
        .then((data) => {
            console.log(data);
            if (!data || data.join_req.length === 0) {
              (inboxIcon.current! as HTMLUListElement).className = "inbox";
            }
            (inboxIcon.current! as HTMLUListElement).className = "inbox new";
        });
  }

  useEffect(newMessage, [])

    return (
      <nav className="HomeNav">
        <ul className="left">
          <li>
            <p onClick={handleLogout}>Logout</p>
          </li>
          <li>
            <Link to="/contact">Contact</Link>
          </li>
          <li>
            <Link to="/wiki">Wiki</Link>
          </li>
        </ul>
        <ul className="right">
        <li className="inbox" ref={inboxIcon}>
           <Link to="/inbox">
                <img className="icon" src="/icons/inbox.png"></img>
           </Link> 
        </li>
          <li>
            <Link to="/classes">Classes</Link>
          </li>
          <li>
            <Link to="/create">
                <button className="register">Create</button>
            </Link>
          </li>
        </ul>
      </nav>
    );
}

export default TeacherNav;
