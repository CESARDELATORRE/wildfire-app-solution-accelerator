#See https://aka.ms/containerfastmode to understand how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS base
WORKDIR /app
EXPOSE 80

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["src/Services/Alerts/RulesEngine/Alerts.RulesEngine.csproj", "src/Services/Alerts/RulesEngine/"]
RUN dotnet restore "src/Services/Alerts/RulesEngine/Alerts.RulesEngine.csproj"
COPY . .
WORKDIR "/src/src/Services/Alerts/RulesEngine"
RUN dotnet build "Alerts.RulesEngine.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "Alerts.RulesEngine.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "Alerts.RulesEngine.dll"]