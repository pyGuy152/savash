import { Link } from "react-router-dom";
import { apiUrl, Class, getToken, loadTheme } from "../types";
import "./HomeNav.css"
import { useRef, useState } from "react";
import "../Register.css";

interface ClassNavProps {
  classSelected: Class;
  inviteModalToggle: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void;
}

function ClassNav({ classSelected, inviteModalToggle }: ClassNavProps) {

  let postRef = useRef < HTMLDialogElement | null>(null);

  let [title, setTitle ] = useState("");
  let [content, setContent] = useState("");

  loadTheme();
  return (
    <nav className="HomeNav">
      <dialog ref={postRef} className="post-create" id="post-create">
        <form className="Register">
          <h2>Create Post</h2>
          <label htmlFor="post-title">Title</label>
          <input 
          onChange={
            (event: React.ChangeEvent<HTMLInputElement>) => {
              setTitle(event.target.value);
            }
          } 
          type="text" id="post-title" name="post-title" required />
          <label htmlFor="post-content">Content</label>
          <textarea 
          onChange={(event: React.ChangeEvent<HTMLTextAreaElement>) => {
            setContent(event.target.value);}
          }
          id="post-content" name="post-content" required></textarea>
          <div className="row">
            <button
              onClick={submitPost}
              className="register"
            >
              Create Post
            </button>
            <button type="button" onClick={togglePostCreate} className="cancel">
              Cancel
            </button>
          </div>
        </form>
      </dialog>

      <ul className="left">
        <li>
          <Link to="/classes">
            <img src="/icons/chevron.png" alt="Back" className="rotate-90deg" />{" "}
            Back
          </Link>
        </li>
      </ul>
      <ul className="center">
        <li>
          <p className="class-title">{classSelected.name}</p>
        </li>
      </ul>
      <ul className="right">
        {localStorage.getItem("role") === "teacher" ? (
          <>
            <li>
              <Link to="./add">
                <button className="register gray">Add Assignment</button>
              </Link>
            </li>
            <li>
              <button onClick={inviteModalToggle} className="register">
                Invite
              </button>
            </li>
          </>
        ) : (
          <></>
        )}
        <li>
          <button className="register" onClick={togglePostCreate}>
            Create Post
          </button>
        </li>
      </ul>
    </nav>
  );

  function togglePostCreate() {
    if (postRef.current) {
      if (postRef.current.open) {
        postRef.current.close();
      } else {
        postRef.current.showModal();
      }
    }
  }

  function submitPost(event: any) {
    event.preventDefault();
    if (postRef.current) {
      postRef.current.close();
    }
    
    fetch(apiUrl + "/classes/" + classSelected.code + "/posts/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "bearer " + getToken(document.cookie),
      },
      body: JSON.stringify({
        title,
        content,
      }),
    })
    }
}

export default ClassNav;