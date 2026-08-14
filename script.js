let currentUserId = null;


// -------------------------
// Register User
// -------------------------

async function registerUser() {

    const name =
        document.getElementById("name").value;

    const email =
        document.getElementById("email").value;


    const response = await fetch(
        "/api/register",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                name: name,
                email: email
            })
        }
    );


    const data = await response.json();

    currentUserId = data.user_id;
}


// -------------------------
// Career Analysis
// -------------------------

async function analyzeCareer() {

    const name =
        document.getElementById("name").value;

    const email =
        document.getElementById("email").value;

    const goal =
        document.getElementById("goal").value;

    const interest =
        document.getElementById("interest").value;


    if (!name || !email) {

        alert(
            "Please enter your name and email."
        );

        return;
    }


    // Register user

    try {

        const registerResponse =
            await fetch(
                "/api/register",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        name: name,
                        email: email
                    })
                }
            );


        const registerData =
            await registerResponse.json();


        if (registerData.user_id) {

            currentUserId =
                registerData.user_id;

        } else {

            // Existing email:
            // use temporary ID for demo

            currentUserId = 1;
        }


    } catch (error) {

        console.error(error);

        alert("Backend connection failed.");

        return;
    }


    // Get selected skills

    const checkboxes =
        document.querySelectorAll(
            ".skills input:checked"
        );


    const skills =
        Array.from(checkboxes)
            .map(
                checkbox =>
                    checkbox.value
            );


    // Send assessment

    try {

        const response =
            await fetch(
                "/api/assessment",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        user_id:
                            currentUserId,

                        skills:
                            skills,

                        interests:
                            [interest],

                        goal:
                            goal

                    })
                }
            );


        const data =
            await response.json();


        displayResults(
            data.recommendations
        );


    } catch (error) {

        console.error(error);

        alert(
            "Could not connect to server."
        );
    }
}


// -------------------------
// Display Results
// -------------------------

function displayResults(results) {

    const container =
        document.getElementById(
            "recommendations"
        );


    container.innerHTML = "";


    results.forEach(
        (result, index) => {

            const div =
                document.createElement(
                    "div"
                );


            div.className = "result";


            const matched =
                result.matched_skills
                    .map(
                        skill =>
                            `<span class="tag">
                                ${skill}
                            </span>`
                    )
                    .join("");


            const missing =
                result.missing_skills
                    .map(
                        skill =>
                            `<span class="tag">
                                ${skill}
                            </span>`
                    )
                    .join("");


            div.innerHTML = `

                <h3>
                    ${index + 1}.
                    ${result.career}
                </h3>

                <div class="score">
                    ${result.score}% Match
                </div>

                <p>
                    <strong>
                        Your Matching Skills:
                    </strong>
                </p>

                <div>
                    ${matched || "None yet"}
                </div>

                <br>

                <p>
                    <strong>
                        Skills You Should Learn:
                    </strong>
                </p>

                <div>
                    ${missing}
                </div>

            `;


            container.appendChild(div);

        }
    );


    document
        .getElementById("results")
        .classList.remove("hidden");


    window.scrollTo({
        top:
            document.body.scrollHeight,
        behavior:
            "smooth"
    });
}