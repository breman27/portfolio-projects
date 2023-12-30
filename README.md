# Portfolio Projects

## Investment Math

This repository contains small projects that showcase various investment-related calculations and concepts. It is designed to be both informative and practical, offering useful tools for everyday financial calculations.

Feel free to explore the different projects and leverage the code for your own purposes. If you have any questions or suggestions, please don't hesitate to reach out.

### How to Run the Project

To run the project, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a Python virtual environment and activate it (optional).
4. Install the necessary dependencies using `pip install -r requirements.txt`.
4. Run the project using `flask run`.


## tls-proxy

The tls-proxy project is a lightweight proxy server that enables secure communication between clients and servers. It acts as an intermediary, encrypting and decrypting TLS traffic to ensure data privacy and integrity. Currently only tested with localhost.

To use this project you can navigate to tls-proxy and run:

1. Create self signed cert using either the go generate_cert tool, or using openssl

2. Add server.local and proxy.local to point to your localhost in your /etc/hosts file

3. Run `go run main.go` in one terminal

4. Run `curl --cacert cert.pem "https://localhost:8080"` (cert.pem may need to be replaced with your cert name/path)

