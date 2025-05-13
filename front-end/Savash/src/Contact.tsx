
import HomeNav from "./components/HomeNav";

import "./Contact.css"

function Contact() {
    return (
      <>
        <HomeNav />
        <main>
          <h1>Wanna tell us something?</h1>
          <h2>Try contacting us</h2>
          <ul>
            <li>Email: rohanjain0725@gmail.com</li>
            <li>
              Discord:
              <a href="https://discord.gg/7wvfjazZ">
                https://discord.gg/7wvfjazZ
              </a>
            </li>
          </ul>
        </main>
      </>
    );
}

export default Contact;