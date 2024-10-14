import React, { useState } from "react";

const PasswordStrengthChecker = () => {
  const [password, setPassword] = useState("");
  const [strength, setStrength] = useState("");

  // Password strength criteria
  const strengthRules = [
    { label: "At least 8 characters", regex: /.{8,}/ },
    { label: "At least one uppercase letter", regex: /[A-Z]/ },
    { label: "At least one lowercase letter", regex: /[a-z]/ },
    { label: "At least one digit", regex: /[0-9]/ },
    { label: "At least one special character", regex: /[^A-Za-z0-9]/ },
  ];

  // Function to check strength
  const checkStrength = (password) => {
    let strengthScore = 0;

    // Iterate over the rules array and increment strengthScore for each passed rule
    strengthRules.forEach((rule) => {
      if (rule.regex.test(password)) strengthScore++;
    });

    // Switch case for strength based on score
    switch (strengthScore) {
      case 0:
      case 1:
      case 2:
        setStrength("Weak");
        break;
      case 3:
        setStrength("Medium");
        break;
      case 4:
        setStrength("Strong");
        break;
      case 5:
        setStrength("Very Strong");
        break;
      default:
        setStrength("Weak");
    }
  };

  const handleChange = (e) => {
    const input = e.target.value;
    setPassword(input);
    checkStrength(input);
  };

  return (
    <div style={{ width: "300px", margin: "10px" }}>
      <h3>Password Strength Checker</h3>
      <input
        type="password"
        value={password}
        onChange={handleChange}
        placeholder="Enter your password"
        style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
      />
      <div
        style={{
          width: "100%",
          height: "10px",
          background: "#e0e0e0",
          marginBottom: "10px",
        }}
      >
        <div
          style={{
            width: `${strength === "Very Strong" ? 100 : strength === "Strong" ? 75 : strength === "Medium" ? 50 : 25}%`,
            height: "100%",
            background:
              strength === "Very Strong"
                ? "green"
                : strength === "Strong"
                ? "orange"
                : strength === "Medium"
                ? "yellow"
                : "red",
          }}
        ></div>
      </div>
      <p>{strength && `Strength: ${strength}`}</p>
    </div>
  );
};

export default PasswordStrengthChecker;
