
import './HomeNav.css';

import { Link } from 'react-router-dom';
import TeacherNav from './TeacherNav';
import StudentNav from './StudentNav';
import { loadTheme } from '../types';

function HomeNav() {
  if(localStorage.getItem("role") === "teacher"){
    return <TeacherNav />
  }
  else if (localStorage.getItem("role") === "student"){
    return <StudentNav />;
  }

  loadTheme();

    return (
      <nav className="HomeNav">
        <ul className="left">
          <Link to="/">
            <img src="logo-medium.png" alt="Savash Logo" className="logo" />
          </Link>
          <li>
            <Link to="/contact">Contact</Link>
          </li>
          <li>
            <Link to="/game">Game?</Link>
          </li>
        </ul>
        <ul className="right">
          <li>
            <Link to="/login">Login</Link>
          </li>
          <li>
            <Link to="/register">
              <button className="register">Register</button>
            </Link>
          </li>
        </ul>
      </nav>
    );
}

export default HomeNav;