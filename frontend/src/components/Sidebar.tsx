import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <aside>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/users">Users</Link>
          </li>
        </ul>
      </nav>
    </aside>
  );
}

export default Sidebar;
