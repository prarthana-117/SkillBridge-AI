"""
============================================================================
SkillBridge AI - Knowledge Base
============================================================================
Everything the AI engine "knows": skills, career roles, learning resources,
interview questions and sample job listings. Edit this file to add new
roles or skills - the rest of the app picks them up automatically.
============================================================================
"""

# ---------------------------------------------------------------------------
# Skills
#   aliases   - words used to detect the skill inside a resume
#   hours     - rough hours to go from zero to job-ready (level 4)
#   resources - free, official learning material
#   project   - a portfolio project idea that proves the skill
# ---------------------------------------------------------------------------
SKILLS = {
    "python": {
        "name": "Python", "category": "Programming",
        "aliases": ["python", "python3"], "hours": 60,
        "resources": [("The Python Tutorial", "https://docs.python.org/3/tutorial/"),
                      ("Python for Everybody", "https://www.py4e.com/")],
        "project": "Build a CLI expense tracker that saves data to a CSV file.",
    },
    "javascript": {
        "name": "JavaScript", "category": "Programming",
        "aliases": ["javascript", "js", "es6", "ecmascript"], "hours": 70,
        "resources": [("MDN JavaScript Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"),
                      ("javascript.info", "https://javascript.info/")],
        "project": "Build an interactive quiz game with a timer and high scores.",
    },
    "typescript": {
        "name": "TypeScript", "category": "Programming",
        "aliases": ["typescript", "ts"], "hours": 30,
        "resources": [("TypeScript Handbook", "https://www.typescriptlang.org/docs/handbook/intro.html")],
        "project": "Convert one of your JavaScript projects to strict TypeScript.",
    },
    "java": {
        "name": "Java", "category": "Programming",
        "aliases": ["java", "jdk", "jvm"], "hours": 80,
        "resources": [("Dev.java Learn", "https://dev.java/learn/")],
        "project": "Build a library management system with OOP classes and file storage.",
    },
    "html_css": {
        "name": "HTML & CSS", "category": "Web",
        "aliases": ["html", "html5", "css", "css3", "flexbox", "tailwind", "bootstrap", "sass"], "hours": 40,
        "resources": [("MDN Learn Web Development", "https://developer.mozilla.org/en-US/docs/Learn"),
                      ("web.dev Learn CSS", "https://web.dev/learn/css")],
        "project": "Recreate a responsive landing page that works on phone and desktop.",
    },
    "react": {
        "name": "React", "category": "Web",
        "aliases": ["react", "reactjs", "react.js", "next.js", "nextjs", "redux"], "hours": 50,
        "resources": [("React Official Docs", "https://react.dev/learn")],
        "project": "Build a movie search app that calls a public API with React hooks.",
    },
    "nodejs": {
        "name": "Node.js", "category": "Web",
        "aliases": ["node", "nodejs", "node.js", "express", "expressjs", "nestjs"], "hours": 45,
        "resources": [("Node.js Learn", "https://nodejs.org/en/learn"),
                      ("Express Guide", "https://expressjs.com/en/guide/routing.html")],
        "project": "Build a REST API for a to-do app with authentication.",
    },
    "rest_api": {
        "name": "REST APIs", "category": "Web",
        "aliases": ["rest", "restful", "rest api", "api", "apis", "graphql", "json"], "hours": 20,
        "resources": [("MDN HTTP Overview", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview")],
        "project": "Design and document a small API with proper status codes and pagination.",
    },
    "sql": {
        "name": "SQL & Databases", "category": "Data",
        "aliases": ["sql", "mysql", "postgresql", "postgres", "sqlite", "database", "databases", "mongodb", "nosql"], "hours": 35,
        "resources": [("SQLBolt Interactive Lessons", "https://sqlbolt.com/"),
                      ("PostgreSQL Tutorial", "https://www.postgresql.org/docs/current/tutorial.html")],
        "project": "Model a college database and write 15 queries with joins and aggregates.",
    },
    "git": {
        "name": "Git & GitHub", "category": "Tools",
        "aliases": ["git", "github", "gitlab", "version control"], "hours": 10,
        "resources": [("Pro Git Book", "https://git-scm.com/book/en/v2"),
                      ("GitHub Skills", "https://skills.github.com/")],
        "project": "Contribute a fix or docs improvement to an open-source repository.",
    },
    "dsa": {
        "name": "Data Structures & Algorithms", "category": "Computer Science",
        "aliases": ["data structures", "algorithms", "dsa", "leetcode", "competitive programming"], "hours": 90,
        "resources": [("CP-Algorithms", "https://cp-algorithms.com/"),
                      ("Open Data Structures", "https://opendatastructures.org/")],
        "project": "Solve 60 problems covering arrays, hashing, trees, graphs and DP.",
    },
    "system_design": {
        "name": "System Design", "category": "Computer Science",
        "aliases": ["system design", "scalability", "microservices", "distributed systems", "architecture"], "hours": 40,
        "resources": [("System Design Primer", "https://github.com/donnemartin/system-design-primer")],
        "project": "Write a design doc for a URL shortener handling 1M requests per day.",
    },
    "testing": {
        "name": "Software Testing", "category": "Tools",
        "aliases": ["testing", "unit testing", "jest", "pytest", "junit", "selenium", "cypress", "tdd"], "hours": 20,
        "resources": [("pytest Docs", "https://docs.pytest.org/"),
                      ("Jest Getting Started", "https://jestjs.io/docs/getting-started")],
        "project": "Add a test suite with 80% coverage to one of your projects.",
    },
    "linux": {
        "name": "Linux & Shell", "category": "Infrastructure",
        "aliases": ["linux", "bash", "shell", "unix", "ubuntu", "shell scripting"], "hours": 25,
        "resources": [("The Linux Command Line", "https://linuxcommand.org/tlcl.php")],
        "project": "Write a shell script that backs up a folder and logs the result daily.",
    },
    "docker": {
        "name": "Docker", "category": "Infrastructure",
        "aliases": ["docker", "containers", "containerization", "docker compose"], "hours": 20,
        "resources": [("Docker Get Started", "https://docs.docker.com/get-started/")],
        "project": "Containerize a web app and its database with Docker Compose.",
    },
    "kubernetes": {
        "name": "Kubernetes", "category": "Infrastructure",
        "aliases": ["kubernetes", "k8s", "helm"], "hours": 35,
        "resources": [("Kubernetes Basics", "https://kubernetes.io/docs/tutorials/kubernetes-basics/")],
        "project": "Deploy a multi-service app to a local Kubernetes cluster (kind/minikube).",
    },
    "cloud": {
        "name": "Cloud (AWS / Azure / GCP)", "category": "Infrastructure",
        "aliases": ["aws", "azure", "gcp", "google cloud", "cloud", "ec2", "s3", "lambda"], "hours": 45,
        "resources": [("AWS Skill Builder", "https://skillbuilder.aws/"),
                      ("Microsoft Learn Azure", "https://learn.microsoft.com/en-us/training/azure/")],
        "project": "Host a static site plus serverless API on a cloud free tier.",
    },
    "cicd": {
        "name": "CI/CD", "category": "Infrastructure",
        "aliases": ["ci/cd", "github actions", "jenkins", "continuous integration", "devops"], "hours": 15,
        "resources": [("GitHub Actions Docs", "https://docs.github.com/en/actions")],
        "project": "Set up a pipeline that tests, builds and deploys on every push.",
    },
    "networking": {
        "name": "Computer Networking", "category": "Infrastructure",
        "aliases": ["networking", "tcp/ip", "tcp", "dns", "http", "subnetting", "network"], "hours": 30,
        "resources": [("Cloudflare Learning Center", "https://www.cloudflare.com/learning/")],
        "project": "Capture and explain a full HTTPS request using Wireshark.",
    },
    "security": {
        "name": "Cybersecurity Fundamentals", "category": "Security",
        "aliases": ["security", "cybersecurity", "owasp", "penetration testing", "siem", "vulnerability", "infosec"], "hours": 50,
        "resources": [("OWASP Top 10", "https://owasp.org/www-project-top-ten/"),
                      ("TryHackMe", "https://tryhackme.com/")],
        "project": "Audit a deliberately vulnerable app (e.g. OWASP Juice Shop) and write a report.",
    },
    "statistics": {
        "name": "Statistics", "category": "Data",
        "aliases": ["statistics", "probability", "hypothesis testing", "a/b testing", "regression"], "hours": 40,
        "resources": [("Khan Academy Statistics", "https://www.khanacademy.org/math/statistics-probability"),
                      ("OpenIntro Statistics", "https://www.openintro.org/book/os/")],
        "project": "Run and report an A/B test analysis on a public dataset.",
    },
    "excel": {
        "name": "Excel / Spreadsheets", "category": "Data",
        "aliases": ["excel", "spreadsheets", "google sheets", "pivot tables", "vlookup"], "hours": 15,
        "resources": [("Microsoft Excel Training", "https://support.microsoft.com/en-us/excel")],
        "project": "Build a sales dashboard with pivot tables and charts.",
    },
    "pandas": {
        "name": "Pandas & NumPy", "category": "Data",
        "aliases": ["pandas", "numpy", "data cleaning", "data wrangling", "jupyter"], "hours": 30,
        "resources": [("pandas Getting Started", "https://pandas.pydata.org/docs/getting_started/index.html"),
                      ("Kaggle Learn Pandas", "https://www.kaggle.com/learn/pandas")],
        "project": "Clean and explore a messy Kaggle dataset in a Jupyter notebook.",
    },
    "data_viz": {
        "name": "Data Visualization & BI", "category": "Data",
        "aliases": ["data visualization", "tableau", "power bi", "matplotlib", "seaborn", "plotly", "dashboards", "looker"], "hours": 25,
        "resources": [("Kaggle Learn Data Visualization", "https://www.kaggle.com/learn/data-visualization"),
                      ("Power BI Training", "https://learn.microsoft.com/en-us/training/powerplatform/power-bi")],
        "project": "Publish an interactive dashboard that answers 3 business questions.",
    },
    "ml": {
        "name": "Machine Learning", "category": "AI",
        "aliases": ["machine learning", "ml", "scikit-learn", "sklearn", "xgboost", "classification", "clustering"], "hours": 80,
        "resources": [("Google ML Crash Course", "https://developers.google.com/machine-learning/crash-course"),
                      ("scikit-learn Tutorials", "https://scikit-learn.org/stable/tutorial/index.html")],
        "project": "Train, evaluate and deploy a model that predicts house prices.",
    },
    "deep_learning": {
        "name": "Deep Learning", "category": "AI",
        "aliases": ["deep learning", "neural networks", "tensorflow", "pytorch", "keras", "cnn", "computer vision"], "hours": 70,
        "resources": [("PyTorch Tutorials", "https://pytorch.org/tutorials/"),
                      ("fast.ai Practical Deep Learning", "https://course.fast.ai/")],
        "project": "Fine-tune an image classifier on your own small dataset.",
    },
    "nlp_llm": {
        "name": "NLP & LLMs", "category": "AI",
        "aliases": ["nlp", "natural language processing", "llm", "llms", "transformers", "hugging face", "prompt engineering", "rag", "generative ai", "genai"], "hours": 40,
        "resources": [("Hugging Face Course", "https://huggingface.co/learn"),
                      ("Prompt Engineering Guide", "https://www.promptingguide.ai/")],
        "project": "Build a chatbot that answers questions about your own documents (RAG).",
    },
    "mlops": {
        "name": "MLOps", "category": "AI",
        "aliases": ["mlops", "mlflow", "model deployment", "model serving", "airflow"], "hours": 30,
        "resources": [("MLOps Zoomcamp", "https://github.com/DataTalksClub/mlops-zoomcamp")],
        "project": "Serve a model behind an API with experiment tracking and monitoring.",
    },
    "figma": {
        "name": "Figma & Prototyping", "category": "Design",
        "aliases": ["figma", "sketch", "adobe xd", "prototyping", "wireframing", "wireframes"], "hours": 20,
        "resources": [("Figma Learn", "https://help.figma.com/hc/en-us/categories/360002051613")],
        "project": "Design a clickable prototype for a mobile food-ordering app.",
    },
    "ux": {
        "name": "UX Design Principles", "category": "Design",
        "aliases": ["ux", "ui/ux", "user experience", "usability", "interaction design", "design systems", "accessibility"], "hours": 40,
        "resources": [("Nielsen Norman Group Articles", "https://www.nngroup.com/articles/"),
                      ("Laws of UX", "https://lawsofux.com/")],
        "project": "Redesign a confusing real-world app screen and document your reasoning.",
    },
    "user_research": {
        "name": "User Research", "category": "Design",
        "aliases": ["user research", "user interviews", "usability testing", "personas", "surveys"], "hours": 20,
        "resources": [("NN/g UX Research Methods", "https://www.nngroup.com/articles/which-ux-research-methods/")],
        "project": "Interview 5 users and turn the findings into personas and a journey map.",
    },
    "product": {
        "name": "Product Management", "category": "Business",
        "aliases": ["product management", "product manager", "roadmap", "prd", "product strategy", "okrs", "kpis"], "hours": 35,
        "resources": [("Atlassian Product Management Guide", "https://www.atlassian.com/agile/product-management")],
        "project": "Write a PRD for a new feature with metrics and a launch plan.",
    },
    "agile": {
        "name": "Agile & Scrum", "category": "Business",
        "aliases": ["agile", "scrum", "kanban", "jira", "sprint"], "hours": 10,
        "resources": [("The Scrum Guide", "https://scrumguides.org/")],
        "project": "Run a 2-week personal project as sprints with a public Kanban board.",
    },
    "communication": {
        "name": "Communication", "category": "Soft Skills",
        "aliases": ["communication", "presentation", "public speaking", "stakeholder management", "writing", "teamwork", "leadership"], "hours": 15,
        "resources": [("Coursera: Improving Communication Skills", "https://www.coursera.org/learn/wharton-communication-skills")],
        "project": "Present one of your projects in a recorded 5-minute demo.",
    },
}

LEVEL_NAMES = {0: "None", 1: "Beginner", 2: "Basic", 3: "Intermediate", 4: "Advanced", 5: "Expert"}

# Weights used for readiness scoring and roadmap priority.
WEIGHTS = {"core": 3, "important": 2, "bonus": 1}

# ---------------------------------------------------------------------------
# Career roles: skill_id -> (target level, weight)
# ---------------------------------------------------------------------------
ROLES = {
    "frontend": {
        "title": "Frontend Developer", "icon": "🎨",
        "summary": "Builds the parts of websites and apps that people see and use.",
        "skills": {"html_css": (4, "core"), "javascript": (4, "core"), "react": (4, "core"),
                   "typescript": (3, "important"), "git": (3, "important"), "rest_api": (3, "important"),
                   "testing": (2, "bonus"), "ux": (2, "bonus"), "communication": (3, "bonus")},
    },
    "backend": {
        "title": "Backend Developer", "icon": "🛠️",
        "summary": "Designs the servers, APIs and databases behind applications.",
        "skills": {"python": (4, "core"), "nodejs": (3, "important"), "sql": (4, "core"),
                   "rest_api": (4, "core"), "git": (3, "important"), "dsa": (3, "important"),
                   "docker": (3, "important"), "system_design": (3, "bonus"), "testing": (3, "bonus"),
                   "linux": (2, "bonus")},
    },
    "fullstack": {
        "title": "Full Stack Developer", "icon": "🧩",
        "summary": "Works across frontend, backend and deployment to ship complete features.",
        "skills": {"html_css": (4, "core"), "javascript": (4, "core"), "react": (3, "core"),
                   "nodejs": (4, "core"), "sql": (3, "important"), "rest_api": (4, "important"),
                   "git": (3, "important"), "docker": (2, "bonus"), "cloud": (2, "bonus"),
                   "testing": (2, "bonus")},
    },
    "data_analyst": {
        "title": "Data Analyst", "icon": "📊",
        "summary": "Turns raw data into insights and dashboards that drive decisions.",
        "skills": {"sql": (4, "core"), "excel": (4, "core"), "data_viz": (4, "core"),
                   "statistics": (3, "important"), "python": (3, "important"), "pandas": (3, "important"),
                   "communication": (4, "important"), "git": (2, "bonus")},
    },
    "data_scientist": {
        "title": "Data Scientist", "icon": "🔬",
        "summary": "Uses statistics and machine learning to answer hard questions with data.",
        "skills": {"python": (4, "core"), "statistics": (4, "core"), "ml": (4, "core"),
                   "pandas": (4, "core"), "sql": (3, "important"), "data_viz": (3, "important"),
                   "deep_learning": (2, "bonus"), "communication": (3, "important"), "git": (2, "bonus")},
    },
    "ml_engineer": {
        "title": "AI / ML Engineer", "icon": "🤖",
        "summary": "Builds, deploys and scales machine-learning and LLM-powered systems.",
        "skills": {"python": (5, "core"), "ml": (4, "core"), "deep_learning": (4, "core"),
                   "nlp_llm": (4, "core"), "mlops": (3, "important"), "docker": (3, "important"),
                   "cloud": (3, "important"), "dsa": (3, "bonus"), "git": (3, "important"),
                   "sql": (2, "bonus")},
    },
    "devops": {
        "title": "DevOps / Cloud Engineer", "icon": "☁️",
        "summary": "Automates infrastructure so software ships quickly and reliably.",
        "skills": {"linux": (4, "core"), "docker": (4, "core"), "kubernetes": (3, "core"),
                   "cloud": (4, "core"), "cicd": (4, "core"), "networking": (3, "important"),
                   "python": (3, "important"), "git": (3, "important"), "security": (2, "bonus")},
    },
    "cybersecurity": {
        "title": "Cybersecurity Analyst", "icon": "🛡️",
        "summary": "Protects systems and data by finding and fixing security weaknesses.",
        "skills": {"security": (4, "core"), "networking": (4, "core"), "linux": (4, "core"),
                   "python": (3, "important"), "cloud": (2, "important"), "sql": (2, "bonus"),
                   "communication": (3, "important")},
    },
    "ux_designer": {
        "title": "UI/UX Designer", "icon": "✏️",
        "summary": "Researches users and designs products that are easy and pleasant to use.",
        "skills": {"ux": (4, "core"), "figma": (4, "core"), "user_research": (4, "core"),
                   "html_css": (2, "bonus"), "communication": (4, "important"),
                   "agile": (2, "bonus")},
    },
    "product_manager": {
        "title": "Product Manager", "icon": "🚀",
        "summary": "Decides what to build and why, and leads teams to ship it.",
        "skills": {"product": (4, "core"), "communication": (5, "core"), "agile": (4, "core"),
                   "user_research": (3, "important"), "data_viz": (2, "important"),
                   "sql": (2, "bonus"), "ux": (2, "bonus")},
    },
}

# ---------------------------------------------------------------------------
# Interview questions: skill_id -> [(question, key points, tip)]
# Key points are short phrases the evaluator looks for in an answer.
# ---------------------------------------------------------------------------
QUESTIONS = {
    "python": [
        ("What is the difference between a list and a tuple in Python?",
         ["mutable", "immutable", "hashable", "performance", "dictionary key"],
         "Mention mutability and when you would pick a tuple (fixed data, dict keys)."),
        ("Explain what a Python decorator is and give a use case.",
         ["function", "wraps", "returns", "logging", "@", "closure"],
         "Describe it as a function that takes a function and returns a new one."),
    ],
    "javascript": [
        ("Explain the difference between let, const and var.",
         ["scope", "block", "function", "hoisting", "reassign", "temporal dead zone"],
         "Cover scope (block vs function), hoisting and reassignment."),
        ("What is a closure in JavaScript?",
         ["function", "scope", "outer", "variables", "remember", "lexical"],
         "A function that remembers variables from its outer (lexical) scope."),
        ("How does the event loop work?",
         ["call stack", "queue", "asynchronous", "callback", "microtask", "promise"],
         "Walk through call stack, task queue and microtasks (promises)."),
    ],
    "react": [
        ("What are React hooks? Explain useState and useEffect.",
         ["state", "side effect", "render", "dependency", "function component", "cleanup"],
         "Explain state updates trigger re-renders and effects run after render."),
        ("Why do lists in React need a key prop?",
         ["unique", "identify", "reconciliation", "re-render", "index"],
         "Keys help React identify which items changed during reconciliation."),
    ],
    "html_css": [
        ("Explain the CSS box model.",
         ["content", "padding", "border", "margin", "box-sizing"],
         "List the four layers and mention box-sizing: border-box."),
        ("When would you use Flexbox vs Grid?",
         ["one-dimensional", "two-dimensional", "rows", "columns", "layout", "alignment"],
         "Flexbox for one direction, Grid for two-dimensional layouts."),
    ],
    "nodejs": [
        ("Why is Node.js good at handling many concurrent connections?",
         ["non-blocking", "event loop", "asynchronous", "single thread", "i/o"],
         "Talk about non-blocking I/O and the event loop."),
        ("What is middleware in Express?",
         ["request", "response", "next", "function", "authentication", "logging"],
         "A function in the request pipeline that can act and call next()."),
    ],
    "rest_api": [
        ("What makes an API RESTful?",
         ["resources", "http methods", "stateless", "status codes", "get", "post"],
         "Resources as URLs, standard HTTP verbs, stateless requests."),
        ("Explain the difference between PUT and PATCH.",
         ["replace", "partial", "update", "idempotent", "entire"],
         "PUT replaces the whole resource; PATCH updates part of it."),
    ],
    "sql": [
        ("What is the difference between INNER JOIN and LEFT JOIN?",
         ["matching", "rows", "both tables", "null", "all rows", "left table"],
         "INNER keeps matches only; LEFT keeps all left rows with NULLs."),
        ("What is an index and when can it hurt performance?",
         ["faster", "lookup", "b-tree", "write", "insert", "storage"],
         "Indexes speed reads but slow writes and use storage."),
        ("Explain GROUP BY and HAVING.",
         ["aggregate", "group", "filter", "where", "count", "sum"],
         "HAVING filters groups after aggregation; WHERE filters rows before."),
    ],
    "git": [
        ("What is the difference between git merge and git rebase?",
         ["history", "commit", "linear", "merge commit", "branch", "rewrite"],
         "Merge preserves history with a merge commit; rebase rewrites for a linear history."),
    ],
    "dsa": [
        ("What is the time complexity of searching in a hash map, and why?",
         ["o(1)", "average", "hash function", "collision", "o(n)", "worst"],
         "Average O(1) thanks to hashing; worst case O(n) with collisions."),
        ("How would you detect a cycle in a linked list?",
         ["two pointers", "fast", "slow", "floyd", "meet", "o(1) space"],
         "Floyd's tortoise and hare: fast and slow pointers meet if there's a cycle."),
    ],
    "system_design": [
        ("How would you design a URL shortener?",
         ["hash", "database", "cache", "redirect", "scale", "unique id", "load balancer"],
         "Cover ID generation, storage, caching, redirects and scaling."),
    ],
    "testing": [
        ("What is the difference between unit and integration tests?",
         ["isolation", "single", "components", "together", "mock", "dependencies"],
         "Unit tests isolate one piece; integration tests check parts working together."),
    ],
    "docker": [
        ("What is the difference between a Docker image and a container?",
         ["template", "read-only", "running", "instance", "layers"],
         "An image is a read-only template; a container is a running instance of it."),
    ],
    "kubernetes": [
        ("What is a Pod and why does Kubernetes use them?",
         ["smallest", "containers", "shared", "network", "storage", "scheduling"],
         "Smallest deployable unit; containers in a pod share network and storage."),
    ],
    "cloud": [
        ("Explain IaaS, PaaS and SaaS with examples.",
         ["infrastructure", "platform", "software", "ec2", "managed", "responsibility"],
         "Compare how much you manage vs the provider manages in each."),
    ],
    "cicd": [
        ("What happens in a typical CI/CD pipeline?",
         ["build", "test", "deploy", "automated", "commit", "artifact"],
         "Walk from a commit through build, tests and automated deployment."),
    ],
    "linux": [
        ("How do Linux file permissions work?",
         ["read", "write", "execute", "owner", "group", "chmod"],
         "Explain rwx for owner/group/others and chmod (e.g. 755)."),
    ],
    "networking": [
        ("What happens when you type a URL into a browser?",
         ["dns", "tcp", "handshake", "tls", "http request", "response", "render"],
         "DNS lookup, TCP + TLS handshake, HTTP request/response, rendering."),
    ],
    "security": [
        ("What is SQL injection and how do you prevent it?",
         ["input", "query", "parameterized", "prepared statements", "sanitize", "validation"],
         "Untrusted input changes the query; use parameterized queries."),
        ("Explain the CIA triad.",
         ["confidentiality", "integrity", "availability"],
         "Name and give an example for each of the three properties."),
    ],
    "statistics": [
        ("Explain what a p-value means.",
         ["probability", "null hypothesis", "observed", "extreme", "significance"],
         "Probability of data this extreme if the null hypothesis is true."),
        ("What is the difference between correlation and causation?",
         ["relationship", "cause", "confounding", "experiment", "variables"],
         "Correlation is association; causation needs controlled evidence."),
    ],
    "excel": [
        ("When would you use a pivot table?",
         ["summarize", "group", "aggregate", "large data", "filter"],
         "To quickly summarize and slice large tables by categories."),
    ],
    "pandas": [
        ("How do you handle missing values in a pandas DataFrame?",
         ["isnull", "dropna", "fillna", "mean", "median", "impute"],
         "Detect with isnull(), then drop or impute depending on context."),
    ],
    "data_viz": [
        ("How do you choose the right chart for your data?",
         ["comparison", "trend", "distribution", "bar", "line", "audience"],
         "Match the chart to the question: comparison, trend, distribution, share."),
    ],
    "ml": [
        ("Explain overfitting and how to prevent it.",
         ["training", "generalize", "validation", "regularization", "cross-validation", "more data"],
         "Model memorizes training data; fix with regularization, CV, more data."),
        ("What is the bias-variance tradeoff?",
         ["bias", "variance", "underfitting", "overfitting", "complexity"],
         "Simple models underfit (high bias), complex ones overfit (high variance)."),
        ("When would you use precision vs recall?",
         ["false positives", "false negatives", "precision", "recall", "f1"],
         "Precision when false positives are costly, recall when misses are costly."),
    ],
    "deep_learning": [
        ("What is backpropagation?",
         ["gradient", "loss", "chain rule", "weights", "update"],
         "Using the chain rule to compute gradients of the loss to update weights."),
    ],
    "nlp_llm": [
        ("What is Retrieval-Augmented Generation (RAG)?",
         ["retrieve", "documents", "embeddings", "context", "vector", "hallucination"],
         "Retrieve relevant documents via embeddings and feed them to the LLM as context."),
        ("What is a transformer's attention mechanism?",
         ["attention", "tokens", "weights", "context", "query", "key", "value"],
         "Each token weighs other tokens using query, key and value vectors."),
    ],
    "mlops": [
        ("How do you monitor a model in production?",
         ["drift", "metrics", "latency", "retrain", "logging", "data quality"],
         "Track data/prediction drift, accuracy, latency; retrain when needed."),
    ],
    "figma": [
        ("How do you use components and auto layout in Figma?",
         ["reusable", "variants", "consistency", "responsive", "auto layout"],
         "Reusable components with variants; auto layout for responsive frames."),
    ],
    "ux": [
        ("Walk me through your design process.",
         ["research", "define", "ideate", "prototype", "test", "iterate"],
         "Research → define problem → ideate → prototype → test → iterate."),
    ],
    "user_research": [
        ("How do you run a usability test?",
         ["tasks", "participants", "observe", "think aloud", "findings", "goals"],
         "Define goals, recruit 5 users, give tasks, observe, synthesize findings."),
    ],
    "product": [
        ("How do you prioritize features?",
         ["impact", "effort", "rice", "users", "goals", "data"],
         "Use a framework like RICE tied to user needs and business goals."),
        ("How would you measure the success of a new feature?",
         ["metrics", "kpi", "adoption", "retention", "baseline", "a/b test"],
         "Define success metrics up front, compare to baseline, run experiments."),
    ],
    "agile": [
        ("What happens in a sprint retrospective?",
         ["went well", "improve", "team", "action items", "reflect"],
         "Team reflects on what went well, what didn't, and agrees on actions."),
    ],
    "communication": [
        ("How do you explain a technical idea to a non-technical person?",
         ["simple", "analogy", "audience", "jargon", "example", "check understanding"],
         "Know your audience, avoid jargon, use analogies, check understanding."),
    ],
}

BEHAVIORAL_QUESTIONS = [
    ("Tell me about a time you faced a difficult problem and how you solved it.",
     ["situation", "task", "action", "result", "learned"],
     "Use the STAR method: Situation, Task, Action, Result."),
    ("Describe a time you worked in a team with a disagreement.",
     ["situation", "listened", "compromise", "action", "result"],
     "Show you listened, stayed respectful and focused on the outcome."),
    ("Tell me about a project you are most proud of.",
     ["goal", "my role", "challenge", "result", "impact"],
     "Be specific about YOUR contribution and a measurable result."),
    ("Why do you want this role?",
     ["interest", "skills", "growth", "company", "goals"],
     "Connect your skills and goals to what the role offers."),
]

# ---------------------------------------------------------------------------
# Sample job listings (fictional companies, for demonstration)
# ---------------------------------------------------------------------------
JOBS = [
    {"id": 1, "title": "Junior Frontend Developer", "company": "PixelCraft Studio", "location": "Bengaluru · Hybrid",
     "type": "Full-time", "role": "frontend", "skills": ["html_css", "javascript", "react", "git"]},
    {"id": 2, "title": "React Developer Intern", "company": "BrightLeaf Labs", "location": "Remote",
     "type": "Internship", "role": "frontend", "skills": ["javascript", "react", "html_css"]},
    {"id": 3, "title": "Backend Engineer (Python)", "company": "Finlytic", "location": "Pune · On-site",
     "type": "Full-time", "role": "backend", "skills": ["python", "sql", "rest_api", "docker", "git"]},
    {"id": 4, "title": "Node.js API Developer", "company": "CloudKart", "location": "Remote",
     "type": "Full-time", "role": "backend", "skills": ["nodejs", "rest_api", "sql", "testing"]},
    {"id": 5, "title": "Full Stack Developer", "company": "EduSpark", "location": "Hyderabad · Hybrid",
     "type": "Full-time", "role": "fullstack", "skills": ["react", "nodejs", "sql", "rest_api", "git"]},
    {"id": 6, "title": "Data Analyst", "company": "RetailIQ", "location": "Mumbai · Hybrid",
     "type": "Full-time", "role": "data_analyst", "skills": ["sql", "excel", "data_viz", "statistics"]},
    {"id": 7, "title": "Business Intelligence Intern", "company": "MetricMint", "location": "Remote",
     "type": "Internship", "role": "data_analyst", "skills": ["excel", "sql", "data_viz"]},
    {"id": 8, "title": "Junior Data Scientist", "company": "HealthAxis", "location": "Chennai · On-site",
     "type": "Full-time", "role": "data_scientist", "skills": ["python", "pandas", "ml", "statistics", "sql"]},
    {"id": 9, "title": "ML Engineer – LLM Apps", "company": "NeuroNest AI", "location": "Bengaluru · Hybrid",
     "type": "Full-time", "role": "ml_engineer", "skills": ["python", "nlp_llm", "deep_learning", "docker", "cloud"]},
    {"id": 10, "title": "DevOps Engineer", "company": "ShipFast Cloud", "location": "Remote",
     "type": "Full-time", "role": "devops", "skills": ["linux", "docker", "kubernetes", "cicd", "cloud"]},
    {"id": 11, "title": "SOC Analyst (L1)", "company": "SecureGrid", "location": "Noida · On-site",
     "type": "Full-time", "role": "cybersecurity", "skills": ["security", "networking", "linux"]},
    {"id": 12, "title": "Product Designer", "company": "Loop Mobility", "location": "Remote",
     "type": "Full-time", "role": "ux_designer", "skills": ["figma", "ux", "user_research", "communication"]},
    {"id": 13, "title": "Associate Product Manager", "company": "Kirana Connect", "location": "Gurugram · Hybrid",
     "type": "Full-time", "role": "product_manager", "skills": ["product", "communication", "agile", "data_viz"]},
    {"id": 14, "title": "Cloud Support Associate", "company": "Nimbus Systems", "location": "Remote",
     "type": "Internship", "role": "devops", "skills": ["linux", "networking", "cloud"]},
]
