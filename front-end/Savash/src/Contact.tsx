import HomeNav from "./components/HomeNav";
import StudentNav from "./components/StudentNav";
import TeacherNav from "./components/TeacherNav";

import "./Contact.css";

function Contact() {
  if (localStorage.getItem("role") === "teacher") {
    <TeacherNav />;
  } else if (localStorage.getItem("role") === "student") {
    <StudentNav />;
  }
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
              href="https://discord.gg/YY6H6tRjAb"
              style={{ textDecoration: "underline" }}
            >
              https://discord.gg/YY6H6tRjAb
            </a>
          </li>
        </ul>
      </main>
    </>
  );
}

export default Contact;
