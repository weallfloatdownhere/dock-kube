FROM golang:1.17-alpine as builder
WORKDIR /go/src/github.com/roman-hds/argo-demo
COPY go.mod ./ 
RUN go mod download
COPY . ./
RUN CGO_ENABLED=0 go build -o /go/bin/argo-demo

FROM alpine:3.13.6
WORKDIR /app
ENV PORT="8080"
COPY --from=builder /go/bin/argo-demo .
ENTRYPOINT [ "/app/argo-demo"]