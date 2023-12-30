package main

import (
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"
	"tls-proxy/listener"
)

func main() {
	// Initialize TLS termination listener
	// This creates a new instance of the TLSTerminationListener struct.
	// It will listen on localhost (127.0.0.1) port 8080, and use cert.pem and key.pem for TLS.
	tlsListener := listener.NewTLSTerminationListener("127.0.0.1", 8080, "cert.pem", "key.pem")

	// Handle graceful shutdown
	// Create a channel to receive OS signals.
	sigCh := make(chan os.Signal, 1)
	// Notify the sigCh channel when we receive an interrupt (SIGINT) or terminate (SIGTERM) signal.
	// This allows the program to clean up and exit gracefully when it's stopped.
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	// Start a goroutine that waits for a signal.
	// When it receives a signal, it prints a message and exits the program.
	// You can add any cleanup code you need before os.Exit(0).
	go func() {
		<-sigCh
		fmt.Println("Shutting down gracefully...")
		// Add cleanup code if necessary
		os.Exit(0)
	}()

	// Start TLS termination listener
	// This starts the listener and blocks until it returns an error.
	// If the listener returns an error, we log the error and exit the program.
	err := tlsListener.Accept()
	if err != nil {
		log.Fatal("Error starting TLS termination listener:", err)
	}
}
