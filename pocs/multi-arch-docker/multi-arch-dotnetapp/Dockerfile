# Learn about building .NET container images:
# https://github.com/dotnet/dotnet-docker/blob/main/samples/README.md

FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:7.0.400 AS build
ARG TARGETARCH

WORKDIR /source

# copy csproj and restore as distinct layers
COPY *.csproj .

RUN dotnet restore -a $TARGETARCH

# copy and publish app and libraries
COPY . .

RUN dotnet publish -a $TARGETARCH --self-contained false --no-restore -o /app

# final stage/image
FROM mcr.microsoft.com/dotnet/runtime:7.0.4
WORKDIR /app
COPY --from=build /app .
ENTRYPOINT ["./dotnetapp"]
