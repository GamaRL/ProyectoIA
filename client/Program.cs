using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Client;
using Blazorise;
using Blazorise.Bootstrap;
using Blazorise.Icons.FontAwesome;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

builder.Services
  .AddSingleton<HttpClient>(
    new HttpClient{BaseAddress = new Uri("http://localhost:8000/")}
  );

builder.Services
  .AddSingleton<IUploadFileService, UploadFileService>();

builder.Services
  .AddSingleton<IAssociationRulesService, AssociationRulesService>();

builder.Services
  .AddBlazorise(options => {
    options.Immediate = true;
  })
  .AddBootstrapProviders()
  .AddFontAwesomeIcons();

await builder.Build().RunAsync();
