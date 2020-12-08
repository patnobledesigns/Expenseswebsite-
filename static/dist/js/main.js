window.onload = function () {
	const usernameField = document.querySelector("#usernameField");
	const feedbackArea = document.querySelector(".invalid_feedback");
	const emailField = document.querySelector("#emailField");
	const emailfeedbackArea = document.querySelector(".emailfeedbackArea");
	const passwordField = document.querySelector("#passwordField");
	const usernameSuccessOutput = document.querySelector(
		".usernameSuccessOutput"
	);
	const showPasswordToggle = document.querySelector(".showPasswordToggle");
	const submitbtn = document.querySelector(".submit-btn");

	const handleToggleInput = (e) => {
		if (showPasswordToggle.innerHTML === `<i class="fas fa-eye"></i> SHOW`) {
			showPasswordToggle.innerHTML = `<i class="fas fa-eye-slash"></i> HIDE`;

			passwordField.setAttribute("type", "text");
		} else {
			showPasswordToggle.innerHTML = `<i class="fas fa-eye"></i> SHOW`;

			passwordField.setAttribute("type", "password");
		}
	};
	showPasswordToggle.addEventListener("click", handleToggleInput);

	emailField.addEventListener("keyup", (e) => {
		const emailVal = e.target.value;
		emailField.classList.remove("is-invalid");
		emailfeedbackArea.style.display = "none";

		if (emailVal.length > 0) {
			var url = "/validate-email/";
			fetch(url, {
				method: "POST",
				body: JSON.stringify({ email: emailVal }),
			})
				.then((res) => res.json())
				.then((data) => {
					console.log(data);
					if (data.email_error) {
						submitbtn.disabled = true;
						emailField.classList.add("is-invalid");
						emailfeedbackArea.style.display = "block";
						emailfeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
					} else {
						submitbtn.removeAttribute("disabled");
					}
				});
		}
	});

	usernameField.addEventListener("keyup", (e) => {
		const usernameVal = e.target.value;

		usernameSuccessOutput.style.display = "block";

		usernameSuccessOutput.textContent = `Checking ${usernameVal}`;

		usernameField.classList.remove("is-invalid");
		feedbackArea.style.display = "none";

		if (usernameVal.length > 0) {
			var url = "/validate-username/";
			fetch(url, {
				method: "POST",
				body: JSON.stringify({ username: usernameVal }),
			})
				.then((res) => res.json())
				.then((data) => {
					console.log(data);
					// setInterval(function() {
					//     usernameSuccessOuput.style.display = "none";
					// },2000)
					usernameSuccessOutput.style.display = "none";
					if (data.username_error) {
						usernameField.classList.add("is-invalid");
						feedbackArea.style.display = "block";
						feedbackArea.innerHTML = `<p>${data.username_error}</p>`;
						submitbtn.disabled = true;
					} else {
						submitbtn.removeAttribute("disabled");
					}
				});
		}
	});
};
