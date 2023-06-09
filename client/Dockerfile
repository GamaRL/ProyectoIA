FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
WORKDIR /src
COPY Client.csproj .
RUN dotnet restore Client.csproj
COPY . .
RUN dotnet build Client.csproj -c Release -o /app/build

FROM build AS publish
RUN dotnet publish Client.csproj -c Release -o /app/publish

EXPOSE 80

FROM nginx:alpine AS final
WORKDIR /usr/share/nginx/html
COPY --from=publish /app/publish/wwwroot .
COPY nginx.conf /etc/nginx/nginx.conf
