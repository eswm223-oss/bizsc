import { Link } from "react-router-dom";

function Header() {
  return (
    <header>
      <nav>
        <Link to="/">Home</Link>
        {"|"}
        <Link to="/users">Users</Link>
      </nav>
    </header>
  );
}

export default Header;
