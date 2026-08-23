import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <div
      className="d-flex flex-column flex-shrink-0 p-3 bg-body-tertiary"
      style={{ width: "250px" }}
    >
      <a
        href="/"
        className="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-body-emphasis text-decoration-none"
      >
        <span className="fs-4">BizSC</span>
      </a>
      <hr />
      <ul className="nav nav-pills flex-column mb-auto">
        <li className="nav-item">
          <Link className="nav-link link-body-emphasis" to="/">
            Home
          </Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link link-body-emphasis" to="/users">
            Users
          </Link>
        </li>
      </ul>
      <hr />
    </div>
  );
}

export default Sidebar;
