import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="bg-light border-end p-3" style={{ width: "130px" }}>
      <nav>
        <ul className="nav flex-column">
          <li className="nav-item">
            <Link className="nav-link" to="/">
              Home
            </Link>
          </li>

          <li className="nav-item">
            <Link className="nav-link" to="/users">
              Users
            </Link>
          </li>
        </ul>
      </nav>
    </aside>
  );
}

export default Sidebar;
