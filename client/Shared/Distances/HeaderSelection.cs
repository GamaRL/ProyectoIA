public class HeaderSelection
{
  public object Header { get; set; }
  public bool IsSelected { get; set; }

  public HeaderSelection(object Header)
  {
    this.Header = Header;
    this.IsSelected = false;
  }
}