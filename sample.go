package main

import (
	"net/http"
)

func main() {
	// 公開するディレクトリを指定する --- (*1)
	fs := http.FileServer(http.Dir("pub"))

	// サーバーURIとの対応を指定 --- (*2)
	http.Handle("/", fs)

	// サーバーの起動 --- (*4)
	http.ListenAndServe(":1323", nil)
}
