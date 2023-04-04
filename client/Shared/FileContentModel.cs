using System.Text.Json.Serialization;

public class FileContentModel
{
  [JsonPropertyName("head")]
  public List<List<string>> Head { get; set; }
  [JsonPropertyName("tail")]
  public List<List<string>> Tail { get; set; }
}