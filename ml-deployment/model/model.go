// model/model.go

package model

import (
	"github.com/cdipaolo/sentiment"
)

// Predict is a placeholder function for a machine learning model.
func Predict(text string) uint8 {
	model, err := sentiment.Restore()
	if err != nil {
		return 0
	}

	analysis := model.SentimentAnalysis(text, sentiment.English)

	return analysis.Score
}
