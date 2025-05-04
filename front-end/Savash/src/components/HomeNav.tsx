
import './HomeNav.css';

import { Link } from 'react-router-dom';

function HomeNav() {
    return (
      <nav className="HomeNav">
        <ul className="left">
          <Link to="/">
            <img src="logo-medium.png" alt="Savash Logo" className="logo" />
          </Link>
          <li>
            <Link to="/pricing">Pricing</Link>
          </li>
          <li>
            <Link to="/contact">Contact</Link>
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