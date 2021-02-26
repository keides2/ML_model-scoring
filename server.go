package main

import (
	//    "net/http"

	"github.com/labstack/echo"
)

func main() {
	e := echo.New()

	// e.GET("/", func(c echo.Context) error {
	//		return c.String(http.StatusOK, "Hello, World!")
	// })

	// 静的ファイルのパスを設定
	e.Static("/", "./pub/")
	e.Static("/data/", "./data/")
	// e.Static("/public/css/", "./public/css")
	// e.Static("/public/js/", "./public/js/")
	// e.Static("/public/img/", "./public/img/")

	e.File("/", "pub/sample.html")
	e.Logger.Fatal(e.Start(":1323"))
}
