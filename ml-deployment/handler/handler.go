// handler/handler.go

package handler

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// IndexHandler handles requests to the index page.
func IndexHandler(c *gin.Context) {
	c.HTML(http.StatusOK, "index.html", nil)
}
