package listener

import (
	"crypto/tls"
	"fmt"
	"net"
)

// TLSTerminationListener represents a custom listener that performs TLS termination.
// It contains the address and port to listen on, and the paths to the certificate and key files for TLS.
type TLSTerminationListener struct {
	Address  string
	Port     int
	CertFile string
	KeyFile  string
}

// NewTLSTerminationListener creates a new TLSTerminationListener instance.
// It takes the address and port to listen on, and the paths to the certificate and key files for TLS.
func NewTLSTerminationListener(address string, port int, certFile, keyFile string) *TLSTerminationListener {
	return &TLSTerminationListener{
		Address:  address,
		Port:     port,
		CertFile: certFile,
		KeyFile:  keyFile,
	}
}

// Accept accepts incoming TLS-encrypted connections.
// It starts a TCP listener on the specified address and port, and handles incoming connections in a separate goroutine.
func (l *TLSTerminationListener) Accept() error {
	addr := fmt.Sprintf("%s:%d", l.Address, l.Port)

	listener, err := net.Listen("tcp", addr)
	if err != nil {
		return err
	}
	defer listener.Close()

	fmt.Printf("Listening on %s\n", addr)

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting connection:", err)
			continue
		}
		fmt.Printf("Incoming connection from %s\n", conn.RemoteAddr())

		// Handle incoming connection (perform TLS termination)
		go l.handleConnection(conn)
	}
}

// handleConnection handles an incoming connection.
// It performs TLS termination on the connection, reads from the connection, and writes a response.
func (l *TLSTerminationListener) handleConnection(conn net.Conn) {
	tlsConn, err := l.terminateTLS(conn)
	defer conn.Close()
	if err != nil {
		// Handle TLS termination error
		fmt.Println("Error terminating TLS:", err)
		return
	}
	defer tlsConn.Close()

	buffer := make([]byte, 1024)

	_, err = tlsConn.Read(buffer)
	if err != nil {
		// Handle read error
		fmt.Println("Error reading from connection:", err)
		return
	}

	fmt.Printf("Received: %s\n", buffer)

	_, err = tlsConn.Write([]byte("HTTP/1.1 200 OK\r\n\r\nHello client, from the listener!\n"))
	if err != nil {
		// Handle write error
		fmt.Println("Error writing to connection:", err)
		return
	}
}

// terminateTLS performs TLS termination on a connection.
// It loads the certificate and key from the specified files, creates a TLS configuration, and performs a TLS handshake.
func (l *TLSTerminationListener) terminateTLS(conn net.Conn) (net.Conn, error) {

	tlsConfig := &tls.Config{
		// Load certificates from CertFile and KeyFile
		Certificates: make([]tls.Certificate, 1),
	}

	cert, err := tls.LoadX509KeyPair(l.CertFile, l.KeyFile)
	if err != nil {
		return nil, err
	}
	tlsConfig.Certificates[0] = cert

	tlsConn := tls.Server(conn, tlsConfig)
	err = tlsConn.Handshake()
	if err != nil {
		return nil, err
	}

	return tlsConn, nil
}
