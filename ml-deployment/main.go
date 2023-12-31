// main.go

package main

import (
	"ml-deployment/handler"
	"ml-deployment/service"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	// Serve HTML page
	router.LoadHTMLGlob("templates/*")
	router.Static("/static", "static")

	router.GET("/", handler.IndexHandler)

	// API endpoint for predictions
	router.POST("/predict", service.PredictHandler)

	// Run the server
	router.Run(":8080")
}
