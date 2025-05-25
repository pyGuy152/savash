import { useNavigate } from "react-router-dom";
import { getToken } from "../types";

const apiUrl = "https://api.codewasabi.xyz";

interface InviteModalProps {
  code: Number;
  closeModal: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void;
}

function InviteModal({ code, closeModal }: InviteModalProps) {
  const navigate = useNavigate();

  function submitForm(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const emailElem = document.getElementById("email") as HTMLInputElement;

    let email = emailElem.value;
    if (emailElem.checkValidity() === false) {
      alert("Please enter a valid email address.");
      return;
    }
    const data = { email };
    console.log(apiUrl);
    fetch(apiUrl + "/classes/" + code + "/invite/", {
      body: JSON.stringify(data),
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "bearer " + getToken(document.cookie),
      },
    }).then(() => {
      navigate("/login");
    });
  }

  return (
    <div className="Register">
      <form onSubmit={submitForm}>
        <h2>Invite A Teacher</h2>
        <label htmlFor="email">Email:</label>
        <input
          type="text"
          name="email"
          id="email"
          required
          pattern="[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
        />
        <br />
        <button type="submit" className="submit">
          Invite
        </button>
      </form>
      <button className="close" onClick={closeModal}>
        Close
      </button>
    </div>
  );
}

export default InviteModal;
