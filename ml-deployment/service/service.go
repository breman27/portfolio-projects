// service/service.go

package service

import (
	"ml-deployment/model"
	"net/http"

	"github.com/gin-gonic/gin"
)

// PredictHandler handles requests to make predictions.
func PredictHandler(c *gin.Context) {
	var input struct {
		Input string `json:"input" binding:"required"`
	}

	if err := c.BindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	prediction := model.Predict(input.Input)

	c.JSON(http.StatusOK, gin.H{"prediction": prediction})
}
