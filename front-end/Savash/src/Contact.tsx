import HomeNav from "./components/HomeNav";

import "./Contact.css";

function Contact() {
  return (
    <>
      <HomeNav />
      <main className="contact">
        <h1>Wanna tell us something?</h1>
        <h2>Try contacting us</h2>
        <ul>
          <li>
            <b>Email:</b> savash@codewasabi.xyz
          </li>
          <li>
            <b>Email:</b> rohanjain0725@gmail.com
          </li>
          <li>
            <b>Discord: </b>
            <a
              href="https://discord.gg/7wvfjazZ"
              style={{ textDecoration: "underline" }}
            >
              https://discord.gg/7wvfjazZ
            </a>
          </li>
        </ul>
      </main>
    </>
  );
}

export default Contact;
